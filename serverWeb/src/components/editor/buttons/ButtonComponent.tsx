import {h, Component, JSX} from "preact";
import {Editor} from "codemirror";
export interface IButtonProps {
 editor?: Editor
}
interface IState {

}
export class ButtonComponent<TProps extends IButtonProps= IButtonProps, TState= IState> extends Component<TProps, TState>{
    shortcut: null| string = null

    componentDidMount() {
        if (this.shortcut && this.props.editor){
            this.props.editor.setOption('extraKeys', {
                ...this.props.editor.getOption('extraKeys'),
                [this.shortcut]: () => this.action(this.props.editor)
            })
        }
    }

    render (props?: TProps, state?: TState) {
        return <button onClick={this.onClick}>{this.icon()}</button>
    }
    private onClick = (e: MouseEvent): void => {
        e.preventDefault()
        this.action(this.props.editor)

    }
    icon (): null|JSX.Element {
        return null
    }
    action (editor?: Editor): void{
        return null
    }
}