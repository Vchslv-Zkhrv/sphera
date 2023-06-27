import {FC} from "react";
import Popup from "../UI/Popup";
import styles from "./Loading.module.css"

interface ILoadingProps {
    visible: boolean
    setVisible: (b: boolean) => void
}


const Loading:FC<ILoadingProps> = ({visible, setVisible}) => {
    return (
        <Popup visible={visible} setVisible={setVisible}>
            <img
                src={require("../../../icons/green/loading.svg").default}
                className={styles.loading}
            />
        </Popup>
    )
}

export default Loading;
