class Socket {
  constructor() {
    const devPort = import.meta.env.WSPORT;
    if (import.meta.env.MODE === 'production') {
      this.port = window.location.port;
    } else {
      this.port = devPort ?? 8000;
    }
    this.socket = null;
    this.callbacks = new Map();
    this.callbacks.set('ERROR', this.defaultErrorHandler);
    this.callbacks.set('CONNECTION_STATE', () => {});
    this.pausedCallbacks = new Map();
    this.retryAttempt = 0;
  }
  get isInitialized() {
    return this.socket?.readyState === WebSocket.OPEN;
  }
  defaultErrorHandler(message) {
    console.warn(message);
  }
  async retryConnection() {
    if (this.isRetrying || this.isInitialized) return;
    this.isRetrying = true;
    this.retryAttempt++;
    const delay = this.retryAttempt;
    console.log(`Retrying connection in ${delay}s...`);
    await new Promise(resolve => setTimeout(resolve, 1000 * delay));
    this.isRetrying = false;
    await this.initSocket();
    if (this.isInitialized) this.retryAttempt = 0;
  }
  async initSocket() {
    return new Promise(resolve => {
      const host = window.location.hostname;
      this.socket = new WebSocket(`ws://${host}:${this.port}/ws`);
      this.socket.onerror = async (err) => {
        this.callbacks.get('CONNECTION_STATE')(false);
        this.callbacks.get('ERROR')('Error connecting to backend. Make sure the server is running.');
        console.warn(err);
        await this.retryConnection();
      };
      this.socket.onclose = async () => {
        this.callbacks.get('CONNECTION_STATE')(false);
        this.callbacks.get('ERROR')('Connection lost. Reconnecting...');
        await this.retryConnection();
      };
      this.socket.onopen = () => {
        this.callbacks.get('CONNECTION_STATE')(true);
        this.setupMessageHandler();
        resolve();
      };
    });
  }
  async ensureSocketConnected() {
    if (!this.isInitialized) {
      await this.initSocket();
    }
  }
  setupMessageHandler() {
    this.socket.onmessage = message => {
      const { payload, status, command } = JSON.parse(message.data);
      const callback = this.callbacks.get(status === 'OK' ? command : 'ERROR');
      if (callback) {
        callback(payload);
      }
    };
  }
  async send(data) {
    await this.ensureSocketConnected();
    this.socket.send(JSON.stringify(data));
  }
  on(event, callback) {
    this.callbacks.set(event, callback);
  }
  pauseListener(event) {
    this.pausedCallbacks.set(event, this.callbacks.get(event));
    this.callbacks.delete(event);
  }
  resumeListener(event) {
    this.callbacks.set(event, this.pausedCallbacks.get(event));
    this.pausedCallbacks.delete(event);
  }
}
const socket = new Socket();
export { socket };
