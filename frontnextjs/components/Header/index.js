import React, {useState} from 'react'
import styles from './index.module.scss';
import {Button} from "@mui/material";
import PtsRequest from "@/components/PtsRequest";

export default function Header() {
    const [openRequest, setOpenRequest] = useState(false)
    const [openShootingPlace, setOpenShootingPlace] = useState(false)
    const [openPtsConfig, setOpenPtsConfig] = useState(false)
    const handleOpenRequest = () => {
        setOpenRequest(true)
        return <PtsRequest />
    }
    const handleOpenShootingPlace = () => {
        setOpenShootingPlace(true)
    }
    const handleOpenPtsConfig = () => {
        setOpenShootingPlace(true)
    }
  return (
      <div className={styles['menu']}>
          <div className={styles['menu-logo']}>LOGO Расписание НГТРК</div>
          <div className={styles['pts-menu-list']}>
          <div className={styles['pts-menu-items']}>
              <Button onClick={handleOpenRequest}>Подать заяву на ПТС</Button> </div>
          <div className={styles['pts-menu-items']}> <Button onClick={handleOpenShootingPlace}>Съемочные площадки</Button></div>
          <div className={styles['pts-menu-items']}> <Button onClick={handleOpenPtsConfig}>Конфигурации ПТС</Button></div>
          <div className={styles['pts-menu-items']}> <Button>Item 4 </Button></div>
          </div>
      </div>
  )
}
