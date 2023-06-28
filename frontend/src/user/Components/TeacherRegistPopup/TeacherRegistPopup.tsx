import {FC, useState, useEffect, MouseEvent, useMemo} from "react"
import Popup from "../UI/Popup"
import styles from "./TeacherRegistPopup.module.css"
import StraightButton from "../UI/StraightButton"
import DimmedButton from "../UI/DimmedButton"
import IndicatorInput from "../UI/IndicatorInput"
import Loading from "../Loading/Loading"
import { UserApi } from "../../userapi"
import Steps from "../UI/Steps"
import { IOption, ITag } from "../../usertypes"
import ChooseOption from "../UI/ChooseOption"
import TagsCloud from "../TagsCloud/TagsCloud"

interface IRegistProps {
    visible: boolean
    setVisible: (b: boolean) => void
}


const TeacherRegistPopup:FC<IRegistProps> = ({setVisible, visible}) => {

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
    const [successMessage, setSccessMessage] = useState<string>("");
    const [currentStep, setCurrentStep] = useState<number>(1)
    
    const [companies, setCompanies] = useState<IOption[]>([]);
    const [selectedCompanies, setSelectedCompanies] = useState<IOption[]>([]);
    const [tags, setTags] = useState<IOption[]>([]);
    const [selectedTags, setSelectedTags] = useState<IOption[]>([]);


    const handleSignUp = async (e: MouseEvent<HTMLButtonElement>) => {
        e.preventDefault();
        
        if (loginCorrect && passwordCorrect && confirmationPasswordCorrect && fnameCorrect && lnameCorrect) {
            if (companies.length===0) {
                setErrorMessage("Укажите компанию")
                return
            }
            else {
                setErrorMessage("")
            }
            setFetching(true)
            setStatus(await UserApi.signupTeacher(
                login,
                password,
                fname,
                lname,
                sname,
                selectedCompanies[0].id,
                selectedTags.map((t) => t.name)
            ))
            if (status===400) {
                setErrorMessage("Логин занят")
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
            setStatus(null);
            setSccessMessage("");
            setSelectedCompanies([]);
            setSelectedTags([]);
            setCurrentStep(1);
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
        confirmationPassword,
    ])

    const fetchTags = async () => {
        setTags(await UserApi.getTags())
    }
    
    const fetchCompanies = async () => {
        setCompanies(await UserApi.getCompanies())
    }

    useEffect(() => {
        fetchCompanies();
        fetchTags()
    }, [])

    return (
        <>
            <Popup visible={visible} setVisible={setVisible}>
                <form className={styles.form}>
                    <h4>
                        {
                            status==204 ?
                            "Успешно" :
                            "Регистрация"
                        }
                    </h4>
                    <p className={styles.success}>
                        {
                            status==204 ?
                            "На вашу электронную почту было отправлено письмо для активации аккаунта" :
                            ""
                        }
                    </p>
                    {
                        status===204 ? <p>{successMessage}</p> :
                        <div className={styles.steps}>
                            <h6>Шаг:</h6>
                            <Steps options={[1, 2, 3]} current={currentStep} setCurrent={setCurrentStep}/>
                        </div>
                    }
                    {
                        status===204 ? <></> 
                        :
                        <div className={styles.pages}>
                        {
                            currentStep===1 ?
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
                        :
                        currentStep===2
                        ?
                        <div>
                            <h6 className={styles.subheader}>Выберите команию</h6>
                            <ChooseOption
                                options={companies}
                                current={selectedCompanies}
                                setCurrent={setSelectedCompanies}
                                checkboxMode={false}
                            />
                        </div>
                        :
                        <div>
                            <h6 className={styles.subheader}>Укажите ваши специальности</h6>
                            <ChooseOption
                                options={tags}
                                current={selectedTags}
                                setCurrent={setSelectedTags}
                                checkboxMode={true}
                            />
                        </div>
                    }
                    </div>
                }
                
                {
                    status===204 ? 
                        <div className={styles.buttons}>
                        <DimmedButton text="Выйти" onClick={handleClose} />
                        </div>
                    :
                        <div className={styles.buttons}>
                        <StraightButton
                            text={currentStep===3 ? "Создать" : "Далее"}
                            onClick={currentStep===3 ? handleSignUp : ()=>{setCurrentStep(currentStep+1)}}/>
                        <DimmedButton text="Выйти" onClick={handleClose} />
                        </div>
                }
                    </form>
                </Popup>
            <Loading setVisible={setFetching} visible={fetching}/>
        </>
    )
}

export default TeacherRegistPopup;
