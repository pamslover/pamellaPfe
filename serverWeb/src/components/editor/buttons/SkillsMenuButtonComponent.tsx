import {h} from  'preact'
import {MenuButtonComponent} from "./MenuButtonComponent";
import {Editor} from "codemirror";

export  default  class SkillsMenuButtonComponent extends MenuButtonComponent{
    shortcut = 'Ctrl-M'
    icon() {
        // @ts-ignore
        return <ion-icon name="add-outline"></ion-icon>;

    }
    action(editor?: Editor) {
        super.action(editor);
    }
}