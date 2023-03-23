import {h, Component, JSX} from "preact";
import {Editor} from "codemirror";
import {ButtonComponent} from "./ButtonComponent";

export interface IButtonProps {
    editor?: Editor
    elements?: ButtonComponent[]
}
interface IState {

}

export class MenuButtonComponent<Tprops extends IButtonProps=IButtonProps, TState= IState > extends Component<Tprops, TState>{
    shortcut: null| string = null

    componentDidMount() {
        if (this.shortcut && this.props.editor){
            this.props.editor.setOption('extraKeys', {
                ...this.props.editor.getOption('extraKeys'),
                [this.shortcut]: () => this.action(this.props.editor)
            })
        }
    }
    render(props?: Tprops, state?: TState) {

        return <div class="menu">
            <div class="toggle" onClick={this.onClick}>
                {this.icon()}
            </div>
            {this.props.elements.map((arrayItem, arrayItemIndex, WholeArray) => (

                <li style={'--i:'+arrayItemIndex+';'}>
                    {arrayItem}
                </li>
            ))}
        </div>
    }
    icon (): null|JSX.Element {
        return null
    }
    action (editor?: Editor): void{
        return null
    }
    getMenu(){
        let menu = document.querySelector('.menu')
        return menu
    }
    private onClick = (e: MouseEvent): void => {
        const menu = this.getMenu()
        const lis = menu.getElementsByTagName('li')
        menu.classList.toggle('active')
        for (var x=0; x< lis.length; x++){
            lis[x].style.setProperty('--nbr_li_element', this.props.elements.length.toString())
        }

        return null

    }
}