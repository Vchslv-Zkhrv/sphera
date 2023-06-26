import { useEffect, useState, FC } from "react";
import styles from "./TagsCloud.module.css";
import { ITag } from "../../usertypes";
import { UserApi } from "../../userapi";
import TagItem from "../UI/TagItem";



interface ITagsCloudProps {
    tags: ITag[]
    setTags: (tag: ITag[]) => void
    selectedTags: ITag[]
    setSelectedTags: (tag: ITag[]) => void
}



const TagsCloud:FC<ITagsCloudProps> = ({tags, setTags, selectedTags, setSelectedTags}) => {

    const onTagSelected = (tag: ITag) => {
        if (!selectedTags.includes(tag)) {
            setSelectedTags([...selectedTags, tag])
        }
        else {
            let copy = [...selectedTags];
            copy.splice(copy.indexOf(tag), 1)
            setSelectedTags([...copy])
        }
    }

    return (
        <div className={styles.cloud}>
            <h5 className={styles.header}>Облако тегов</h5>
            <button className={styles.clear} onClick={() => {setSelectedTags([])}}>Сбросить</button>
            <ul className={styles.list}>
                {
                    tags.map((tag) => (
                        <TagItem
                            tag={tag}
                            isChecked={selectedTags.includes(tag)}
                            callback={onTagSelected}
                            key={tag.id}
                        />
                    ))
                }
            </ul>
        </div>
    )
}

export default TagsCloud;
