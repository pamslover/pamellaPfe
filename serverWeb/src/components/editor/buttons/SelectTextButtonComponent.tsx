import {h} from  'preact'
import {ButtonComponent,IButtonProps} from "./ButtonComponent";
import {Editor} from "codemirror";

interface IProps  extends IButtonProps{
    showFileManager: boolean,
    onClick: () => void
}
export default class SelectTextButtonComponent extends ButtonComponent<IProps>{

    icon() {
        let {showFileManager} = this.props
        let style = showFileManager ? 'fill:#8BC34A':''
        return <svg fill="#000000" width="800px" height="800px" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
            <path fill-rule="evenodd" d="M15,3.41421356 L15,7 L18.5857864,7 L15,3.41421356 Z M19,9 L15,9 C13.8954305,9 13,8.1045695 13,7 L13,3 L5,3 L5,21 L19,21 L19,9 Z M5,1 L15.4142136,1 L21,6.58578644 L21,21 C21,22.1045695 20.1045695,23 19,23 L5,23 C3.8954305,23 3,22.1045695 3,21 L3,3 C3,1.8954305 3.8954305,1 5,1 Z M11,13 L11,10 L13,10 L13,13 L16,13 L16,15 L13,15 L13,18 L11,18 L11,15 L8,15 L8,13 L11,13 Z" style={style}/>
        </svg>
    }
    action(editor: Editor) {
        this.props.onClick()
    }
}