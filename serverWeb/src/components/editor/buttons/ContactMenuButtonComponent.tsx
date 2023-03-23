import {h} from "preact";
import { MenuButtonComponent} from "./MenuButtonComponent";
import {Editor} from "codemirror";

export default class ContactMenuButtonComponent extends MenuButtonComponent{
    shortcut = 'Ctrl-T'
    icon() {
        // @ts-ignore
        return <ion-icon name="business-outline"></ion-icon>;

    }
    action(editor?: Editor) {
        super.action(editor);
    }
}