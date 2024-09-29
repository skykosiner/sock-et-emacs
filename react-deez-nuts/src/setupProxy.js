const { createProxyMiddleware } = require('http-proxy-middleware');

module.exports = function(app) {
    app.use(
        "/api",
        createProxyMiddleware({
            target: "http://backend:8081",
            changeOrigin: true,
        })
    );
};
