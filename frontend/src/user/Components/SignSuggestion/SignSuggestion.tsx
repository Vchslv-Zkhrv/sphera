import {FC, useEffect, useState} from "react"
import styles from "./SignSuggestion.module.css"
import LoginPopup from "../LoginPopup/LoginPopup";
import SelectCreatingRole from "../SelectCreatingRole/SelectCreatingRole";


const SignSuggestion:FC = () => {

    const [signInVisible, setSignInVidible] = useState<boolean>(false);
    const [signUpVisible, setSignUpVidible] = useState<boolean>(false);

    return (
        <div className={styles.island}>

            <LoginPopup visible={signInVisible} setVisible={setSignInVidible}/>
            <SelectCreatingRole visible={signUpVisible} setVisible={setSignUpVidible}/>

            <button
                className={styles.button}
                onClick={() => {setSignInVidible(true)}}
            >
                <img src={require("../../../icons/green/fingerprint.svg").default} />
                <p>Войти</p>
            </button>
            <button
                className={styles.button}
                onClick={() => {setSignUpVidible(true)}}
            >
            <img src={require("../../../icons/green/rocket.svg").default} />
                <p>Создать аккаунт</p>
            </button>
        </div>
    )
}

export default SignSuggestion;
