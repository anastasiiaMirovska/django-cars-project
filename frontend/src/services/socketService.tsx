import {authService} from "./authService";
import {w3cwebsocket as W3cwebsocket} from "websocket";
const baseURL = 'ws://test-django.eu-north-1.elasticbeanstalk.com/api'

const socketService = async()=>{
    const {data:{token}} = await authService.getSocketToken();
    return {
        chat: (room:string)=>new W3cwebsocket(`${baseURL}/chat/${room}?token=${token}`),
        car: ()=>new W3cwebsocket(`${baseURL}/cars/?token=${token}`)
    }

}
export{
    socketService
}