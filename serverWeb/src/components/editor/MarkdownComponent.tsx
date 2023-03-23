import {h,Component} from "preact";
import {marked} from "marked";
interface IProps {
    markdown: string
}
interface IState {

}
export default class MarkdownComponent extends Component<IProps, IState>{
    constructor(props: IProps) {
        super();
        marked.setOptions({
            gfm: true,
            breaks: false,
            sanitize: false,
            smartLists: true,
            smartypants: false,
        })
    }
    render () {
         return <div dangerouslySetInnerHTML={{__html: this.html}}> </div>
    }
    get html(): string {
       return  marked(this.props.markdown)
    }
}