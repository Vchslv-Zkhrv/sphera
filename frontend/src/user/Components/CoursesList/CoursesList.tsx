import {FC} from "react"
import styles from "./CoursesList.module.css";
import { ICourseCard } from "../../usertypes";
import CourseCard from "../CourseCard/CourseCard";



const CoursesList:FC<{courses: ICourseCard[]}> = ({courses}) => {
    return (
        <ul className={styles.list}>
            { courses.map((c) => (
                <div className={styles.courseWithHr}>
                    <CourseCard {...c} key={c.id}/>
                    <hr className={styles.hr} />
                </div>
                
            )) }
        </ul>
    )
}

export default CoursesList;
