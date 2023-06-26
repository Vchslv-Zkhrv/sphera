import {FC} from "react"
import { INewsParagraph } from "../../usertypes";
import styles from "./Paragraph.module.css"

const Paragraph:FC<INewsParagraph> = ({id, content, kind}) => {
    return (
        <div>
            {
                kind==="image src" ?
                <img src={content} alt={`${id}`} className={styles.cover}/>
                :
                <p className={styles.text}>{content}</p>
            }
        </div>
    )
}

export default Paragraph;
