import {h, Component, JSX} from "preact";
import CodeMirrorComponent from "./CodeMirrorComponent";
import './style.scss'
import MarkdownComponent from "./MarkdownComponent";
import * as CodeMirror from "codemirror";
import {Bold, Italic, FullScreen, Speech, Joy, Menu, ContactMenu, ShowFileManager} from "./buttons";
import {ISections, SectionsGenerator} from "./libs/SectionsGenerator";
import {debounce} from "lodash";
import {FileManager} from 'filemanager-element'
import 'filemanager-element/FileManager.css'

FileManager.register();

interface IProps {
    value: string |null
    name: string |null
}
interface IState {
    content: string
    editor: CodeMirror.Editor| null
    fullscreen: boolean
    showFileManager: boolean
}
interface IEditorSections {
    editor: ISections
    preview: ISections
    [key: string]:ISections
}
export default class Editor extends Component<IProps, IState>{
    private sections: IEditorSections|null = null
    private scrollingSection: string|null = null
    private $editor?: HTMLElement
    private $preview?: HTMLElement


    constructor(props: IProps) {
        super(props);
        this.state = {
            content: props.value || '',
            editor: null,
            fullscreen: false,
            showFileManager:false
        }
    }


    componentDidMount() {
        window.addEventListener('resize',this.resetSections)
        const script = document.createElement("script");
        const script1 = document.createElement("script");
        script.type = "module"
        script.src = "https://unpkg.com/ionicons@5.5.2/dist/ionicons/ionicons.esm.js";
        script1.noModule
        script1.src = "https://unpkg.com/ionicons@5.5.2/dist/ionicons/ionicons.js";
        script.async = true;
        script1.async = true;
        document.body.appendChild(script1);
        document.body.appendChild(script1);
    }

    componentWillUnmount() {
        window.removeEventListener('resize', this.resetSections)
    }

    componentDidUpdate(previousProps: IProps, previousState: IState, snapshot: any) {

        if(previousState.fullscreen !== this.state.fullscreen){
            if(this.state.editor){
                this.state.editor.refresh()
            }
        }
        if (previousState.content !== this.state.content){
            this.sections = null
        }
        this.sections = null
        // @ts-ignore
        this.$editor = this.base.querySelector('.mdeditor__editor') as HTMLDivElement
        // @ts-ignore
        this.$preview = this.base.querySelector('.mdeditor__preview') as HTMLDivElement
    }
    getSections(): IEditorSections|null{
        if (this.sections === null && this.$editor && this.$preview){
            this.sections = {
                editor : SectionsGenerator.fromElement(this.$editor),
                preview : SectionsGenerator.fromElement(this.$preview)
            }
        }
        return this.sections
    }
    private resetSections = () => {
        this.sections = null
    }
    render({name}:IProps,{content, editor, fullscreen, showFileManager}:IState): JSX.Element {
        let cls = 'mdeditor'
        const filemanager = document.querySelector('file-manager')
        if (fullscreen){
            cls += ' mdeditor--fullscreen'
        }
       if (showFileManager){
            filemanager.removeAttribute('hidden')
        }
        filemanager.addEventListener('close', () =>{
            filemanager.setAttribute('hidden', '')
            this.toggleshowfilemanager()
        })
        const menu1_item = []
        menu1_item.push(<Bold editor={editor}/>)
        menu1_item.push(<Italic editor={editor}/>)
        menu1_item.push(<Speech editor={editor}/>)
        menu1_item.push(<Bold editor={editor}/>)
        menu1_item.push(<Italic editor={editor}/>)
        menu1_item.push(<Speech editor={editor}/>)
        // use menu component
        const contactMenuList = []
        contactMenuList.push(<Speech editor={editor}/>)
        contactMenuList.push(<Bold editor={editor}/>)
        contactMenuList.push(<Italic editor={editor}/>)


        return <div class={cls}>
            <div class="mdeditor__toolbar">
                <div class="mdeditor__toolbarleft">
                    {editor && [
                        <Bold editor={editor}/>,
                        <Italic editor={editor}/>,
                        <Speech editor={editor}/>,
                        <Joy editor={editor}/>,
                    ]}
                </div>
                <div className="mdeditor__toolbarcenter">
                    {editor && [
                        <Menu editor={editor} elements={menu1_item}/>,
                        //<ContactMenu editor={editor} elements={contactMenuList}></ContactMenu>
                    ]}
                </div>
                <div class="mdeditor__toolbarright">
                    {editor && [
                        <ShowFileManager showFileManager={showFileManager} onClick={this.toggleshowfilemanager}/>,
                        <FullScreen fullscreen = {fullscreen} onClick={this.togglefullscreen}/>,
                    ]}
                </div>
            </div>
            <div class="mdeditor__editor" onScroll={this.onScroll}>
                <CodeMirrorComponent value={content} onReady={this.setEditor}/>
            </div>
            <div class="mdeditor__preview" onScroll={this.onScroll}>
                <MarkdownComponent markdown={content}/>
            </div>
            <textarea name={name || ''} style="display:none">{content}</textarea>
        </div>
    }
    setEditor = (editor: CodeMirror.Editor): void => {
        this.setState({editor})
        editor.on('change',  (e) => {
            this.setState({content: e.getDoc().getValue()})
        })
    }
    togglefullscreen = () =>{
        this.setState({fullscreen: !this.state.fullscreen})
    }
    toggleshowfilemanager = () =>{
        this.setState({showFileManager: !this.state.showFileManager})
    }
    onScroll = (e: UIEvent) =>{
        let sections = this.getSections()
        if(sections === null){
            return
        }
        let eventTarget = e.target as HTMLDivElement;
        let source = eventTarget === this.$editor ? 'editor' : 'preview'
        if (this.scrollingSection === null){
            this.scrollingSection = source
        }else if(this.scrollingSection !== source){
            return;
        }
        let target = source === 'editor' ? 'preview' : 'editor'
        let $source = eventTarget
        let $target = eventTarget === this.$editor ? this.$preview : this.$editor
        let scrollTop = SectionsGenerator.getScrollTop($source.scrollTop, sections[source], sections[target])
        if ($target){
            $target.scrollTop = scrollTop
        }
        this.resetScrolling()
    }
    private resetScrolling = debounce(()=>{
        this.scrollingSection = null
    }, 500)
}