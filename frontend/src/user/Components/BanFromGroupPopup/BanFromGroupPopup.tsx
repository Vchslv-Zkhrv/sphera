import {FC} from "react";
import Popup from "../UI/Popup";
import StraightButton from "../UI/StraightButton";
import DimmedButton from "../UI/DimmedButton";
import styles from "./BanFromGroup.module.css"
import { UserApi } from "../../userapi";

interface IBanPopup {
    sid: number | null
    gid: number | null
    fname: string
    lname: string
    visible: boolean
    setVisible: (b: boolean) => void
    updateCallback: () => void
}


const BanFromGroupPopup:FC<IBanPopup> = ({
    sid, gid, visible, setVisible, fname, lname, updateCallback}) => {

    const handleDelete = async () => {
        if (gid && sid) {
            await UserApi.banFromGroup(gid, sid)
            updateCallback()
            setVisible(false)
        }
    }

    return (
        <Popup visible={visible} setVisible={setVisible}>
            <h2>{fname} {lname}</h2>
            <div className={styles.buttons}>
                <StraightButton text="Удалить" onClick={() => {handleDelete()}}/>
                <DimmedButton text="Отмена" onClick={() => {setVisible(false)}} />
            </div>
        </Popup>
    )
}

export default BanFromGroupPopup;
