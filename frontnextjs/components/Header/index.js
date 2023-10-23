import React from 'react'
import styles from './index.module.scss';
import Image from 'next/image';
import {Typography} from "@mui/material";
import Link from "next/link";

export default function Header() {
  return (
      <div className={styles['menu']}>
          <div className={styles['menu-logo']}>
            <Image
              src="/image/logo.png"
              alt="Logo"
              width={300}
              height={50}
              
            />
          </div>
          <div className={styles['menu-list']}>
            <div className={styles['menu-items']}>
              <Link href="/createrequest">
                  <Typography>Create Request</Typography>
              </Link>
            </div>
          <div className={styles['menu-items']}>Площадки </div>
          <div className={styles['menu-items']}>Конфигурации </div>
          <div className={styles['menu-items']}> Выйти </div>
          </div>
      </div>
  )
}
