import {h} from  'preact'
import {ButtonComponent, IButtonProps} from "./ButtonComponent";
import {Editor} from "codemirror";

interface Istate {
    listening:boolean
}
interface Iprops extends IButtonProps{
    editor: Editor
}
export default class SpeechButtonComponent extends ButtonComponent<Iprops, Istate>{
    recognition?: SpeechRecognition
    constructor(props: Iprops) {
        super(props);
        if (window.hasOwnProperty('webkitSpeechRecognition')){
            this.recognition = new webkitSpeechRecognition()
            this.recognition.lang = 'fr-FR'
            this.recognition.continuous = true
            this.recognition.interimResults = false
        }
        this.state = {
            listening : false
        }
    }

    icon() {
        console.log(this.recognition)
        if (this.recognition === undefined) return null

        let {listening} = this.state
        let style = listening ? 'fill:#FF0000' : ''
        return <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 384 512" ><path d="M96 256V96c0-53.019 42.981-96 96-96s96 42.981 96 96v160c0 53.019-42.981 96-96 96s-96-42.981-96-96zm252-56h-24c-6.627 0-12 5.373-12 12v42.68c0 66.217-53.082 120.938-119.298 121.318C126.213 376.38 72 322.402 72 256v-44c0-6.627-5.373-12-12-12H36c-6.627 0-12 5.373-12 12v44c0 84.488 62.693 154.597 144 166.278V468h-68c-6.627 0-12 5.373-12 12v20c0 6.627 5.373 12 12 12h184c6.627 0 12-5.373 12-12v-20c0-6.627-5.373-12-12-12h-68v-45.722c81.307-11.681 144-81.79 144-166.278v-44c0-6.627-5.373-12-12-12z" style={style}/></svg>    }

    action(editor: Editor) {
        console.log('make action')
        if(this.recognition === undefined){
            return
        }
        if(this.state.listening){
            console.log('stop mic')
            this.recognition.stop()
            this.setState({listening:false})
            return;
        }
        this.recognition.start()
        this.setState({listening:true})
        this.recognition.onresult = (e)=>{
            let result = e.results.item(e.resultIndex)
            console.log(e)
            if (result.isFinal === true){
                let transcript = result.item(0).transcript
                if (this.shouldCapitalize()){
                    transcript = this.capitalize(transcript)
                }
                editor.getDoc().replaceSelection(transcript)
            }
        }

        // console.log(this.recognition)
    }
    shouldCapitalize(): boolean {
        let cursor = this.props.editor.getDoc().getCursor()
        let sentence = this.props.editor.getDoc().getRange({
            line: cursor.line,
            ch: 0
        }, cursor).trim()
        return cursor.ch === 0 || sentence.endsWith('.')
    }
    capitalize(s: string): string{
        return s.charAt(0).toUpperCase() + s.slice(1)
    }
}

/**
 * this.recognition.onresult = (e)=>{
            let result = e.results.item(e.resultIndex)
            console.log(e)
            if (result.isFinal === true){
                let transcript = result.item(0).transcript
                editor.getDoc().replaceSelection(transcript)
            }
        }
 * */