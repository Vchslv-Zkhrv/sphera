import {FC} from "react"
import Popup from "../UI/Popup"


interface IUnlockProps {
    visible: boolean
    setVisible: (b: boolean) => void
}


const UnlockPopup:FC<IUnlockProps> = ({visible, setVisible}) => {
    return (
        <Popup visible={visible} setVisible={setVisible}>
            <img/>
        </Popup>
    )
}