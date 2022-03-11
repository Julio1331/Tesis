const express = require('express')
const { Socket } = require('socket.io')
const app = express()
//const routes = require('./routes/littlezoom.routes.js')

//crea servidos http a partir de express
const http = require ('http').Server(app)
//para generar comunicacion se trabaja con socket.io
const io = require('socket.io')(http)
//routes
app.use(require('./routes/littlezoom.routes'))
//app.use(routes)
//donde se cargaran los html
app.use(express.static(__dirname + '/public'))

//crea el canal de comunicacion
io.on('connection',(socket)=>{
    socket.on('stream',(image)=>{
        //emitir el evento a todos los sockets conectados
        socket.broadcast.emit('stream', image)
    })
})
module.exports = http