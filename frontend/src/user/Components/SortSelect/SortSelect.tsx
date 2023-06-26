import {FC, useState} from "react"
import styles from "./SortSelect.module.css"
import SortOption from "../UI/SortOption";


interface ISortSelectProps {
    sort: string
    setSort: (s: string) => void
    sortDesc: boolean
    setSortDesc: (b: boolean) => void
}


const SortSelect:FC<ISortSelectProps> = ({sort, setSort, setSortDesc, sortDesc}) => {

    return (
        <div className={styles.wrapper}>
            <div className={styles.sort}>
                <SortOption value="random" text="Случайно" active={sort==="random"} callback={setSort} />
                <SortOption value="views" text="По просмотрам" active={sort==="views"} callback={setSort} />
                <SortOption value="name" text="По названию" active={sort==="name"} callback={setSort} />
                <SortOption value="date" text="По дате" active={sort==="date"} callback={setSort} />
            </div>
            <div className={styles.sort}>
                <SortOption
                    value={false}
                    text="По возрастанию"
                    active={!sortDesc}
                    callback={setSortDesc}
                    disabled={sort==="random"}
                />
                <SortOption
                    value={true}
                    text="По убыванию"
                    active={sortDesc}
                    callback={setSortDesc}
                    disabled={sort==="random"}
                />
            </div>
        </div>
    )
}


export default SortSelect;
