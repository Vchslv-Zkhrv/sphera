import {FC, HTMLAttributes} from "react"
import styles from "./HiddenScroll.module.css";

const HiddenScroll:FC<HTMLAttributes<HTMLDivElement>> = (props) => {
    return (
        <section {...props} className={`${props.className} ${styles.section}`}>
            {props.children}
        </section>
    )
}

export default HiddenScroll;
