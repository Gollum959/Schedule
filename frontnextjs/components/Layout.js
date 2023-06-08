import React from 'react';
import Head from "next/head";
import Header from "@/components/Header";


const Layout = ({ children }) => {
  return (
    <>
    <Head>
        <title>Расписание НГТРК</title>
        <meta
          name="description"
          content="Расписание ПТС НГТРК"
        />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" href="/favicon.ico" />
      </Head>
    	<Header />
    	<main>{children}</main>
    </>
  )
}

export default Layout;