import {FC, useEffect, useState} from "react"
import Popup from "../UI/Popup"
import { IGroup, IOption } from "../../usertypes"
import { UserApi } from "../../userapi"
import styles from "./ChooseGroupPopup.module.css"



interface IChooseGroupPopupProps {
    visible: boolean
    setVisible: (b: boolean) => void
    courseId: any
}


const ChooseGroupPopup:FC<IChooseGroupPopupProps> = ({visible, setVisible, courseId}) => {

    const [groups, setGroups] = useState<IGroup[]>([]);

    const fetchGroups =async () => {
        setGroups(await UserApi.getGroups())
    }

    useEffect(() => {
        fetchGroups()
    }, [])

    const handleClick = async (id: number) => {
        await UserApi.startGroupSession(id, courseId);
        setVisible(false);
        document.location.pathname = "/groups"
    }

    return (
        <Popup visible={visible} setVisible={setVisible}>
            <div className={styles.wrapper}>
                <h1>Выберите группу</h1>
                <ul>
                {
                    groups.map((g) => (
                        <li key={g.id} className={styles.group} onClick={() => {handleClick(g.id)}}>
                            {g.name}
                        </li>
                    ))
                }
                </ul>
            </div>
        </Popup>
    )
}


export default ChooseGroupPopup;
