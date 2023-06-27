import {FC, HTMLAttributes, ReactElement, ReactNode} from "react"
import styles from "./Popup.module.css";


interface IPopupProps {
    visible: boolean
    setVisible: (b: boolean) => void
    children: ReactNode | ReactElement
}


const Popup:FC<IPopupProps> = ({visible, setVisible, children}) => {

    const handleSeaClick = () => {
        setVisible(false);
    }

    const handleIslandClick = (e: React.MouseEvent<HTMLDivElement>) => {
        e.stopPropagation()
        e.preventDefault()
    }

    return (
        <div
            className={!visible ? styles.hide : styles.sea }
            onClick={() => {handleSeaClick()}}
        >
            <div
                className={styles.island} 
                onClick={handleIslandClick}>
                {children}
            </div>
        </div>
    )
}


export default Popup;
