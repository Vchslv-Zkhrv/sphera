import {FC, useEffect, useState, MouseEvent, useContext} from "react"
import Popup from "../UI/Popup"
import StraightInput from "../UI/StraightInput"
import StraightButton from "../UI/StraightButton"
import DimmedButton from "../UI/DimmedButton"
import styles from "./LoginPopup.module.css"
import SwitchRole from "../UI/SwitchRole"
import { UserContext } from "../../usercontext"
import { UserApi } from "../../userapi"

interface ILoginProps {
    visible: boolean
    setVisible: (b: boolean) => void
}


const LoginPopup:FC<ILoginProps> = ({visible, setVisible}) => {

    const {user, setUser} = useContext(UserContext);

    const [login, setLogin] = useState<string>("");
    const [password, setPassword] = useState<string>("");
    const [role, setRole] = useState<"student" | "teacher">("student")
    const [errorMessage, setErrorMessage] = useState<string>(" ");

    const handleSignIn = async (e: MouseEvent<HTMLButtonElement>) => {
        e.preventDefault();
        setUser(await UserApi.auth(login, password, role));
        if (user===null) { 
            setErrorMessage("Данные неверны")
        }
    }

    const handleClose = (e: MouseEvent<HTMLButtonElement>) => {
        e.preventDefault();
        setVisible(false);
    }

    useEffect(() => {
        setLogin("");
        setPassword("");
        setRole("student");
        setErrorMessage(" ");
    }, [visible])
    

    return (
        <Popup visible={visible} setVisible={setVisible}>
            <form className={styles.form}>
                <h4>Войти в систему</h4>
                <p>{errorMessage}</p>
                <div className={styles.fields}>
                    <StraightInput
                        type_="text"
                        value={login}
                        setValue={setLogin}
                        placeholder="Логин"
                    />
                    <StraightInput
                        type_="password"
                        value={password}
                        setValue={setPassword}
                        placeholder="Пароль"
                    />
                    <div className={styles.switch}>
                        <SwitchRole role={role} setRole={setRole}/>
                    </div>
                </div>
                <div className={styles.buttons}>
                    <StraightButton text="Войти" onClick={handleSignIn}/>
                    <DimmedButton text="Отмена" onClick={handleClose}/>
                </div>
            </form>

        </Popup>
    )
}


export default LoginPopup;
