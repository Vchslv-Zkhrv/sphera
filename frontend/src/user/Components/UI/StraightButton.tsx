import { FC, useContext} from "react";
import { UserContext } from "../../usercontext";
import styles from "./StraightButton.module.css";

interface IButtonProps {
    text: string
    onClick: (e: React.MouseEvent<HTMLButtonElement, MouseEvent>) => void
}


const StraightButton:FC<IButtonProps> = ({text, onClick}) => {

    const {user, setUser} = useContext(UserContext);
    

    return (
        <button
            onClick={(e) => onClick(e)}
            className={user===null ? styles.main : user.role==="student" ? styles.main : styles.alter}
        >
            {text}
        </button>
    )
}

export default StraightButton;
