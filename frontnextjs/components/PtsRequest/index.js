import React, {useState} from 'react'
import styles from './index.module.scss';


export default function Footer() {

  return (
      <div className={styles['footer']}>
          {/*<div className={styles['footer-logo']}>LOGO</div>*/}
          <div className={styles['footer-text-wrapper']}>
          <div className={styles['footer-text-items']}>
              Создано Alex&Alex</div>
          <div className={styles['footer-text-items']}> @Все права защищенны 2023 </div>

          </div>
      </div>
  )
}
