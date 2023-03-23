export type ISection = [number,number]
export type ISections = ISection[]

let selectors: string[] = []
for (let i=1; i<6; i++){
    selectors.push(`h${i}`, `.cm-header-${i}`)
}
export class SectionsGenerator {
     static fromElement(element: HTMLElement): ISections{
        let titles = element.querySelectorAll(selectors.join(',')) as NodeListOf<HTMLElement>
        let start = 0
        let sections:ISections = []
        titles.forEach((title) =>{
            let offsetTop = this.offsetTop(title, element)
            sections.push([start, offsetTop])
            start = offsetTop
        })
        sections.push([start, element.scrollHeight])
        return sections
    }
    private static  offsetTop(element: HTMLElement,target:HTMLElement, acc = 0): number{
        if (element === target){
            return acc
        }
        return this.offsetTop(element.offsetParent as HTMLElement, target, acc + element.offsetTop)
    }
    private static getIndex(position:number, sections: ISections): number{
        return sections.findIndex(function (section) {
            return position >= section[0] && position <= section[1]
        })
    }
    static getScrollTop(position: number, sourceSections: ISections, targetSections:ISections): number{
        let index = this.getIndex(position, sourceSections)
        let source = sourceSections[index]
        let percentage = (position -source[0]) / (source[1] - source[0])
        let target = targetSections[index]
        return target[0] + percentage *(target[1] - target[0])
    }
}