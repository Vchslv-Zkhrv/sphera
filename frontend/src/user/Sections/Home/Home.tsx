import {FC} from "react"
import HiddenScroll from "../../Components/UI/HiddenScroll";
import styles from "./Home.module.css";

const Home:FC = () => {
    return (
        <HiddenScroll>
            <div className={styles.feed}>
                <h1>Новости</h1>
            </div>
        </HiddenScroll>
    )
}


export default Home;
