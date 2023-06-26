import {FC, useEffect, useState} from "react"
import HiddenScroll from "../../Components/UI/HiddenScroll";
import styles from "./Home.module.css";
import { INews } from "../../usertypes";
import { UserApi } from "../../userapi";
import News from "../../Components/News/News";

const Home:FC = () => {

    const [news, setNews] = useState<INews[]>([]);

    const fetchNews = async () => {
        setNews(await UserApi.getFeed())
    }

    useEffect(() => {
        fetchNews()
    }, [])

    return (
        <HiddenScroll>
            <div className={styles.home}>
                <h1>Новости</h1>
                <div className={styles.feed}>
                    {
                        news.map((n) => ( <News {...n} key={n.id}/>))
                    }
                </div>
            </div>
        </HiddenScroll>
    )
}


export default Home;
