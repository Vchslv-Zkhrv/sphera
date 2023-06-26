import {FC} from "react"
import { ITag } from "../../usertypes"
import styles from "./TagItem.module.css";

interface IITagProps {
    isChecked: boolean
    callback: (tag: ITag) => void
    tag: ITag
}


const TagItem:FC<IITagProps> = ({tag, isChecked, callback}) => {

    return (
        <button
            className={isChecked ? styles.buttonActive : styles.button}
            onClick={() => {callback(tag)}}
        >
            {tag.name}
        </button>
    )
}

export default TagItem;
