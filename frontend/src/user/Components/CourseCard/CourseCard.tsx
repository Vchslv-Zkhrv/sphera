import {FC} from "react"
import { ICourseCard } from "../../usertypes"
import styles from "./CourseCard.module.css"

const CourseCard:FC<ICourseCard> = ({id, name, tags, views}) => {
    return (
        <div className={styles.card}>
            <div>
                <h4>{name}</h4>
                <p>{views} просмотров</p>
            </div>
            <ul className={styles.tagsCloud}>
                {
                    tags.map((t) => (
                        <li key={t.id} className={styles.tag}>
                            {t.name}
                        </li>
                    ))
                }
            </ul>
        </div>
    )
}


export default CourseCard;
