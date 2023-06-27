import {FC, useState, useMemo} from "react";
import StraightButton from "./StraightButton";
import styles from "./CopyLink.module.css";


interface ICopyLinkProps {
    callback: () => Promise<string | null>
    text: string
}


const CopyLink:FC<ICopyLinkProps> = ({text, callback}) => {

    const [url, setUrl] = useState<string | null>(null);

    const handleClick = async () => {
        const resp = await callback()
        setUrl(resp)
    }

    useMemo(() => {
        if (url) {
            console.log(url)
            navigator.clipboard.writeText(url);
        }
    }, [url])

    return (
        <div>
        {
            url===null
            ?
            <StraightButton text={text} onClick={() => {handleClick()}}/>
            :
            <p className={styles.done}>Ссылка скопирована</p>
        }
        </div>
    )
}


export default CopyLink;
