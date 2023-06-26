import {FC, useEffect, useMemo, useState} from "react"
import styles from "./Explore.module.css"
import CoursesList from "../../Components/CoursesList/CoursesList";
import TagsCloud from "../../Components/TagsCloud/TagsCloud";
import SortSelect from "../../Components/SortSelect/SortSelect";
import { ICourseCard, ITag } from "../../usertypes";
import { UserApi } from "../../userapi";


const Explore:FC = () => {

    const [tags, setTags] = useState<ITag[]>([]);
    const [selectedTags, setSeletedTags] = useState<ITag[]>([]);
    const [sort, setSort] = useState<string>("random");
    const [sortDesc, setSortDesc] = useState<boolean>(false);
    const [courses, setCourses] = useState<ICourseCard[]>([]);

    const fetchTags = async() => {
        setTags(await UserApi.getTags())
    }

    const fetchCourses = async () => {
        setCourses(await UserApi.searchCourses(
            [...selectedTags.map((t) => t.id)],
            sort,
            sortDesc
        ))
    }

    useEffect(() => {
        fetchTags()        
    }, [])

    useEffect(() => {
        fetchCourses()
    }, [selectedTags, sort, sortDesc])

    return (
        <section className={styles.explore}>
            <div className={styles.main}>
                <SortSelect
                    setSort={setSort}
                    sort={sort}
                    sortDesc={sortDesc}
                    setSortDesc={setSortDesc}
                />
                {
                    courses.length>0
                    ?
                    <CoursesList courses={courses}/>
                    :
                    <h5 className={styles.nothing}>К сожалению, ничего не нашлось</h5>
                }
            </div>
            <TagsCloud
                tags={tags}
                setTags={setTags}
                selectedTags={selectedTags}
                setSelectedTags={setSeletedTags}
            />
        </section>
    )
}


export default Explore;
