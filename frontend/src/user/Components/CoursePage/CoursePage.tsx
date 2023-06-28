import {FC, useContext, useEffect, useState} from "react"
import styles from "./CoursePage.module.css"
import { ICourse, ILessonShort, ITag, IUserContext, IUserShort } from "../../usertypes"
import { UserApi } from "../../userapi"
import Loading from "../Loading/Loading"
import { useParams } from "react-router-dom"
import { UserContext } from "../../usercontext"
import StraightButton from "../UI/StraightButton"
import ChooseGroupPopup from "../ChooseGroupPopup/ChooseGroupPopup"

const CoursePage:FC = () => {

    const {user, setUser} = useContext(UserContext);

    const {courseId} = useParams(); 

    const [id, setId] = useState<number>();
    const [name, setName] = useState<string>("");
    const [description, setDescription] = useState<string>("");
    const [tags, setTags] = useState<ITag[]>([]);
    const [author, setAuthor] = useState<IUserShort>({id: 0, fname: "", lname: ""});
    const [dateCreated, setDateCreated] = useState<string>("");
    const [dateUpdated, setDateUpdated] = useState<string>("");
    const [views, setViews] = useState<number>();
    const [lessons, setLessons] = useState<ILessonShort[]>([]);

    const [groupVisible, setGroupVisible]  = useState<boolean>(false)

    const [status, setStatus] = useState<number>();

    const [loadingVisible, setLoadingVisible] = useState<boolean>(false);

    const fetchCourse = async () => {
        setLoadingVisible(true)
        const resp = await UserApi.getCourse(courseId)
        setStatus(resp.status)
        if (resp.ok) {
            const data:ICourse = await resp.json()
            setName(data.name)
            setTags(data.tags)
            setAuthor(data.author)
            setDateCreated(data.date_created.toString())
            setDateUpdated(data.date_updated.toString())
            setId(data.id)
            setViews(data.views)
            setDescription(data.description)
            setLessons(data.lessons)
        }
        setLoadingVisible(false)
    }

    useEffect(() => {
        fetchCourse()

    }, [courseId])

    
    return (
        <>
            {
                status===undefined ? <></> :
                status!==200 ?  <h1 className={styles.notFound}>Не найдено</h1> :
                <div className={styles.course}>
                    <h1> {name} </h1> 
                    <ul className={styles.tags}>
                        {tags.map((t) => (
                            <li className={styles.tag} key={t.id}>{t.name}</li>
                        ))}
                    </ul>
                    <div className={styles.fields}>
                        <div className={styles.field}>
                            <img  className={styles.fieldIcon} src={require("../../../icons/green/comment-alt.svg").default}/>
                            <p className={styles.fieldContent}> {description} </p>
                        </div>
                        <div className={styles.field}>
                            <img  className={styles.fieldIcon} src={require("../../../icons/green/brain-circuit.svg").default}/>
                            <p className={styles.fieldContent}> {author.fname} {author.lname} </p>
                        </div>
                        <div className={styles.field}>
                            <img  className={styles.fieldIcon} src={require("../../../icons/green/eye.svg").default}/>
                            <p className={styles.fieldContent}> {views} </p>
                        </div>
                    </div>
                    <div>
                        {
                            user?.role==="student" ?
                            <StraightButton text="Начать изучение" onClick={() => {}}/>
                            :
                            user?.role==="teacher" ?
                            <StraightButton text="Начать изучение в группе" onClick={() => {setGroupVisible(true)}} />
                            :
                            <></>
                        }
                    </div>
                    <ul className={styles.lessons}>
                        {lessons.map((l) => (
                            <li key={l.id} className={styles.lesson}>
                                {l.number}. {l.name}
                            </li>
                        ))}
                    </ul>
                </div>

            }
            <ChooseGroupPopup visible={groupVisible} setVisible={setGroupVisible} courseId={courseId}/>
            <Loading visible={loadingVisible} setVisible={setLoadingVisible}/>
        </>
    )
}

export default CoursePage;
