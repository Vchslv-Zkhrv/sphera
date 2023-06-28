import {FC, useContext, useState, useEffect} from "react"
import { IGroup, ISession } from "../../usertypes";
import { UserContext } from "../../usercontext";
import styles from "./GroupCard.module.css";
import StraightButton from "../UI/StraightButton";
import CopyLink from "../UI/CopyLink";
import { UserApi } from "../../userapi";
import BanFromGroupPopup from "../BanFromGroupPopup/BanFromGroupPopup";



interface IGroupCardProps {
    group: IGroup
    updateCallback: () => void
}



const GroupCard:FC<IGroupCardProps> = ({group, updateCallback}) => {

    const {user, setUser} = useContext(UserContext);

    const [expanded, setExpanded] = useState<boolean>(false);
    const [banVisible, setBanVisible] = useState<boolean>(false);
    const [banId, setBanId] = useState<number | null>(null);
    const [banFname, setBanFname] = useState<string>("");
    const [banLname, setBanLname] = useState<string>("");

    const [sessions, setSessions] = useState<ISession[]>([]);

    const fetchLink = async () => {
        const url = await UserApi.getJoinGropLink(group.id)
        return url;
    }

    const fetchSessions =async ( ) => {
        setSessions(await UserApi.getGroupSessions(group.id))
    }

    const handleClickStudent = (id:number, fname:string, lname:string) => {
        if (user?.role==="teacher") {
            setBanId(id);
            setBanFname(fname);
            setBanLname(lname);
            setBanVisible(true);
        }
    }

    return (
        <div className={styles.card}>

            <BanFromGroupPopup
                gid={group.id}
                sid={banId}
                lname={banLname}
                fname={banFname}
                visible={banVisible}
                setVisible={setBanVisible}
                updateCallback={updateCallback}
            />

            <div className={styles.header} onClick={() => {setExpanded(!expanded)}}>
                <h3>{group.name}</h3>
            </div>
            <div>
                {
                    expanded ?
                    <div className={styles.content}>
                        <div className={styles.membersWrapper}>
                            <h5>Участники</h5>
                            <ul className={styles.members}>
                                {
                                    user!==null && user.role!=="teacher" ? 
                                    <li
                                        className={styles.teacher}
                                        >
                                        {group.teacher.fname} {group.teacher.lname}
                                    </li>
                                    : <></>
                                } 
                                {
                                    group.students.map((s) => (
                                        <li
                                            className={
                                                s.id==user?.id
                                                ? styles.studentMe
                                                : user?.role==="teacher"
                                                    ? styles.student4Teacher
                                                    : styles.student
                                            }
                                            onClick={() => {handleClickStudent(s.id, s.fname, s.lname)}}
                                        >
                                            {s.fname} {s.lname}
                                        </li>
                                    ))
                                }
                            </ul>
                            {
                                user?.role === "teacher" ?
                                <div className={styles.buttons}>
                                    <StraightButton text="Добавить студента" onClick={() => {}}/>
                                    <CopyLink callback={fetchLink} text="Сгенерировать ссылку-приглашение"/>
                                </div>
                                :
                                <></>
                            }
                        </div>
                        <div className={styles.sessionsWrapper}>
                            <h5>Курсы</h5>
                            <ul className={styles.sessions}>
                                {sessions.map((s) => (
                                    <li key={s.id}>
                                        <p>{s.course.name}</p>
                                        <p>Старт {s.date_started.toString()}</p>
                                        {
                                            !s.date_ended ?
                                            <p>Не завершено</p> :
                                            <p>Завершено {s.date_ended.toString()}</p>
                                        }
                                    </li>
                                ))}
                            </ul>                            
                        </div>
                    </div>
                    :
                    <></>
                }
            </div>
        </div>
    )
}


export default GroupCard;
