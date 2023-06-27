import {FC, useContext, useEffect, useState} from "react"
import { IGroup } from "../../usertypes";
import { UserApi } from "../../userapi";
import styles from "./Classes.module.css";
import StraightButton from "../../Components/UI/StraightButton";
import CreateGroupPopup from "../../Components/CreateGroupPopup/CreateGroupPopup";
import { UserContext } from "../../usercontext";
import GroupCard from "../../Components/GroupCard/GroupCard";

const Classes:FC = () => {

    const {user, setUser} = useContext(UserContext);
    const [groups, setGroups] = useState<IGroup[]>([]);
    const [createGroupVisible, setCreateGroupVisible] = useState<boolean>(false);

    const fetchGroups = async () => {
        setGroups(await UserApi.getGroups())
    }

    useEffect(() => {
        fetchGroups()
    }, [])

    return (
        <section className={styles.classes}>
            
            <CreateGroupPopup visible={createGroupVisible} setVisible={(b) => {setCreateGroupVisible(b)}}/>

            <header className={styles.header}>
                <h1>Мои классы</h1>
                {
                    user===null ? <></> :
                    user.role==="teacher" ?
                    <StraightButton text="Создать" onClick={() => {setCreateGroupVisible(true)}}/>
                    : <></>
                }
            </header>

            {
                groups.length === 0
                ?
                <div>
                    <h6>
                        {
                            user ? "Вы не состоите ни в одном классе"
                            : "Войдите в аккаунт, чтобы продолжить"
                        }
                    </h6>
                </div>
                :
                <div className={styles.groups}>
                {
                    groups.map((g) => (
                        <GroupCard group={g} updateCallback={fetchGroups} key={g.name}/>
                    ))
                }
                </div>
            }
        </section>
    )
}


export default Classes;
