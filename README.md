# Sock et emacs
* It's pronounced suck it emacs btw
    * Btw I use vim

# Basic overview
* This is a small project that can control my lights using [Home Assistant](https://www.home-assistant.io/), [Neovim](https://github.com/neovim/neovim), and computer in general
* It uses websocket server in typescript to communicate vim commands to python
    * Python then goes through and process the info, if it's all good it will send it down a TCP server to my neovim instance that's connected to the server and will then process the command every 5 seconds in a que
