# %%
import streamlit as st 
import pandas as pd
import time
import duckdb

st.title("마당 서점 관리 시스템 ver. DuckDB")

con = duckdb.connect(database='madang_store.db')   

def query(sql):
    return con.execute(sql).fetchall()


books = [None]
result = query("SELECT concat(bookid, ',', bookname) FROM Book")
for res in result:
    books.append(res[0])

tab1, tab2 = st.tabs(["고객 조회", "거래 입력"])

name = ""
result = pd.DataFrame()
name = tab1.text_input("고객명")
select_book = ""


# ==================================
# 고객 조회
# ==================================

if len(name) > 0:
    sql = f"""
    SELECT c.custid, c.name, b.bookname, o.orderdate, o.saleprice
    FROM Customer c, Book b, Orders o
    WHERE c.custid = o.custid
      AND b.bookid = o.bookid
      AND c.name = '{name}'
    """
    result = con.execute(sql).fetchdf()

    tab1.write(result)
    custid = result['custid'][0]
    
    tab2.write("고객번호: " + str(custid))
    tab2.write("고객명: " + name)

    select_book = tab2.selectbox("구매 서적", books)

    if select_book is not None:
        bookid = select_book.split(',')[0]
        dt = time.localtime()
        dt = time.strftime('%Y-%m-%d', dt)

        orderid = query("SELECT max(orderid) FROM Orderws")[0][0] + 1

        price = tab2.text_input("금액")

        sql = f"""
        INSERT INTO Orders(orderid, custid, bookid, saleprice, orderdate)
        VALUES ({orderid}, {custid}, {bookid}, {price}, '{dt}')
        """

        if tab2.button("거래 입력"):
            con.execute(sql)
            con.commit()
            tab2.write("거래가 입력되었습니다.")


