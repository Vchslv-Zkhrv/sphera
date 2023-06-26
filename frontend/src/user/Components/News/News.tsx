import {FC, useState} from "react";
import { INews, INewsParagraph } from "../../usertypes";
import styles from "./News.module.css";
import { UserApi } from "../../userapi";
import Paragraph from "../Paragraph/Paragraph";

const News:FC<INews> = ({id, date, title}) => {

    const [expanded, setExpanded] = useState<boolean>(false);
    const [paragraphs, setParagraphs] = useState<INewsParagraph[]>([]);

    const fetchParagraphs = async () => {
        setParagraphs(await UserApi.getNews(id));
    }


    const handleClick = () => {
        if (!expanded && paragraphs.length===0) {
            fetchParagraphs()
        }
        setExpanded(!expanded)
    }

    return (
        <div className={styles.news}>
            <div className={styles.head} onClick={() => {handleClick()}}>
                <h3>{title}</h3>
                <p>{date.toString()}</p>
            </div>
            {
                expanded ? 
                <div className={styles.content}>
                    { paragraphs.map((p) => (<Paragraph {...p} key={p.id}/>)) }
                </div>
                : <></>
            }
            
        </div>
    )
}

export default News;
