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
  }
  get isInitialized() {
    return this.socket?.readyState === WebSocket.OPEN;
  }
  defaultErrorHandler(message) {
    console.warn(message);
  }
  async initSocket() {
    return new Promise(resolve => {
      const host = window.location.hostname;
      this.socket = new WebSocket(`ws://${host}:${this.port}/ws`);
      this.setupMessageHandler();
      this.socket.onopen = () => resolve();
      this.socket.onerror = err => {
        const callback = this.callbacks.get('ERROR');
        callback('Error connecting to backend. Make sure the server is running.');
        console.warn(err);
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
}
const socket = new Socket();
export { socket };
