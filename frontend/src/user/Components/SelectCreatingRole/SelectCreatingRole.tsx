import {FC, useEffect, useState} from "react";
import Popup from "../UI/Popup";
import StraightButton from "../UI/StraightButton";
import DimmedButton from "../UI/DimmedButton";
import styles from "./SelectCreatingRole.module.css"
import StudentRegistPopup from "../StudentRegistPopup/StudentRegistPopup";
import TeacherRegistPopup from "../TeacherRegistPopup/TeacherRegistPopup";

interface ISelectRoleProps {
    visible: boolean
    setVisible: (b: boolean) => void
}


const SelectCreatingRole:FC<ISelectRoleProps> = ({visible, setVisible}) => {

    const [studentVisible, setStudentVisible] = useState<boolean>(false);
    const [teacherVisible, setTeacherVisible] = useState<boolean>(false);

    const handleStudent = () => {
        setVisible(false);
        setStudentVisible(true);
    }

    const handleTeacher = () => {
        setVisible(false);
        setTeacherVisible(true);
    }

    return (
        <>

            <StudentRegistPopup visible={studentVisible} setVisible={setStudentVisible}/>
            <TeacherRegistPopup visible={teacherVisible} setVisible={setTeacherVisible}/>

            <Popup visible={visible} setVisible={setVisible}>
                <h4>Создание аккаунта</h4>
                <div className={styles.roles}>
                    <StraightButton text="Для студента" onClick={handleStudent}/>    
                    <StraightButton text="Для преподаватея" onClick={handleTeacher}/>
                </div>
                <div className={styles.exit}>
                    <DimmedButton text="Отмена" onClick={() => {setVisible(false)}} />
                </div>
            </Popup>
        </>
    )
}


export default SelectCreatingRole;
