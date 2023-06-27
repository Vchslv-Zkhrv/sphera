import {FC, useState, MouseEvent, useEffect} from "react"
import Popup from "../UI/Popup"
import StraightInput from "../UI/StraightInput"
import StraightButton from "../UI/StraightButton"
import DimmedButton from "../UI/DimmedButton"
import styles from "./CreateGroupPopup.module.css"

interface ICreateGroupProps {
    visible: boolean
    setVisible: (b: boolean) => void
}


const CreateGroupPopup:FC<ICreateGroupProps> = ({visible, setVisible}) => {

    const [name, setName] = useState<string>("");

    const handleSubmit = (e: MouseEvent<HTMLButtonElement>) => {
        e.preventDefault()
    }

    const handleReject = (e: MouseEvent<HTMLButtonElement>) => {
        e.preventDefault()
        setVisible(false)
    }

    useEffect(() => {
        setName("");
    }, [visible])


    return (
        <Popup visible={visible} setVisible={setVisible}>
            <h3>Создание класса</h3>
            <form className={styles.form}>
                <div className={styles.field}>
                    <p>Введите название</p>
                    <StraightInput value={name} setValue={setName} type_="text"/>
                </div>
                <div className={styles.buttons}>
                    <StraightButton text="Создать" onClick={handleSubmit}/>
                    <DimmedButton text="Отмена" onClick={handleReject} />
                </div>
            </form>
        </Popup>
    )
}

export default CreateGroupPopup;
