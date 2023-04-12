import {h, render} from 'preact'
import Editor from "./components/editor";
/*import {FileManager} from 'filemanager-element'
import 'filemanager-element/FileManager.css'

FileManager.register();*/
let textareas = document.querySelectorAll('textarea.mdeditor') as NodeListOf<HTMLTextAreaElement>
textareas.forEach(function (textarea) {
    let value = textarea.value
    let name = textarea.getAttribute('name')
    let div = document.createElement('div')
    if (textarea.parentNode){
        textarea.parentNode.replaceChild(div, textarea)
        render(<Editor name={name} value={value}/>, div)
    }

})
if(module.hot){
    module.hot.accept(function(){
       window.location.reload()

    })
}

