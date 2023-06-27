import {FC, useState, useEffect, MouseEvent, useMemo} from "react"
import Popup from "../UI/Popup"
import styles from "./StudentRegistPopup.module.css"
import StraightButton from "../UI/StraightButton"
import DimmedButton from "../UI/DimmedButton"
import IndicatorInput from "../UI/IndicatorInput"
import Loading from "../Loading/Loading"
import { UserApi } from "../../userapi"


interface IRegistProps {
    visible: boolean
    setVisible: (b: boolean) => void
}


const StudentRegistPopup:FC<IRegistProps> = ({setVisible, visible}) => {

    const [errorMessage, setErrorMessage] = useState<string>("  ");
    const [login, setLogin] = useState<string>("");
    const [loginCorrect, setLoginCorrect] = useState<boolean>(false);
    const [password, setPassword] = useState<string>("");
    const [passwordCorrect, setPasswordCorrect] = useState<boolean>(false);
    const [confirmationPassword, setConfirmationPassword] = useState<string>("");
    const [confirmationPasswordCorrect, setConfirmationPasswordCorrect] = useState<boolean>(false);
    const [fname, setFname] = useState<string>("")
    const [fnameCorrect, setFnameCorrect] = useState<boolean>(false);
    const [lname, setLname] = useState<string>("")
    const [lnameCorrect, setLnameCorrect] = useState<boolean>(false);
    const [sname, setSname] = useState<string>("")

    const [status, setStatus] = useState<number | null>(null);
    const [fetching, setFetching] = useState<boolean>(false);

    
    const handleSignUp = async (e: MouseEvent<HTMLButtonElement>) => {
        e.preventDefault();
        if (loginCorrect && passwordCorrect && confirmationPasswordCorrect && fnameCorrect && lnameCorrect) {
            setFetching(true)
            setStatus(await UserApi.signupStudent(login, password, fname, lname, sname))
            if (status == 400) {
                setErrorMessage("Логин занят")
            }
            if (status == 204) {
                
            }
            setFetching(false)
        }
    }

    const handleClose = (e: MouseEvent<HTMLButtonElement>) => {
        e.preventDefault();
        setVisible(false);
    }

    useEffect(() => {
        setLogin("");
        setPassword("");
        setErrorMessage("  ");
        setConfirmationPassword("");
        setFname("");
        setLname("");
        setSname("");
    }, [visible])


    
    useMemo(()=> {
        if (!login.includes("@") || !login.includes(".") || login.length < 10) { setLoginCorrect(false); }
        else { setLoginCorrect(true) }

        if (fname) { setFnameCorrect(true) }
        else {setFnameCorrect(false)}

        if (lname) { setLnameCorrect(true) }
        else {setLnameCorrect(false)}

        if (password.length > 5) { setPasswordCorrect(true) }
        else {setPasswordCorrect(false)}

        if (confirmationPassword.length > 5) {
            if (confirmationPassword==password) {
                setConfirmationPasswordCorrect(true);
                setErrorMessage("");
            }
            else {
                setConfirmationPasswordCorrect(false);
                setErrorMessage("Пароли не совпадают")
            }
        }
        else {setConfirmationPasswordCorrect(false)}
        
    }, [
        login,
        fname,
        lname,
        sname,
        password,
        confirmationPassword
    ])

    return (
        <>
            <Popup visible={visible} setVisible={setVisible}>
                <form className={styles.form}>
                    <h4>Регистрация</h4>
                    <p>{errorMessage}</p>
                    <div className={styles.fields}>
                        <IndicatorInput
                            type_="text"
                            value={login}
                            setValue={setLogin}
                            placeholder="Эл. почта"
                            isCorrect={loginCorrect}
                            />
                        <IndicatorInput
                            type_="text"
                            value={lname}
                            setValue={setLname}
                            placeholder="Фамилия"
                            isCorrect={lnameCorrect}
                            />
                        <IndicatorInput
                            type_="text"
                            value={fname}
                            setValue={setFname}
                            placeholder="Имя"
                            isCorrect={fnameCorrect}
                            />
                        <IndicatorInput
                            type_="text"
                            value={sname}
                            setValue={setSname}
                            placeholder="Отчество"
                            isCorrect={true}
                        />
                        <IndicatorInput
                            type_="password"
                            value={password}
                            setValue={setPassword}
                            placeholder="Пароль"
                            isCorrect={passwordCorrect}
                            />
                        <IndicatorInput
                            type_="password"
                            value={confirmationPassword}
                            setValue={setConfirmationPassword}
                            placeholder="Введите пароль еще раз"
                            isCorrect={confirmationPasswordCorrect}
                            />
                    </div>
                    <div className={styles.buttons}>
                        <StraightButton text="Создать аккаунт" onClick={handleSignUp}/>
                        <DimmedButton text="Выйти" onClick={handleClose} />
                    </div>
                </form>
            </Popup>
            <Loading setVisible={setFetching} visible={fetching}/>

        </>
    )
}

export default StudentRegistPopup;
