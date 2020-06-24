package main

import (
	"encoding/json"
	"fmt"
	"strconv"
)


type KeepZero float64


func (f KeepZero) MarshalJSON() ([]byte, error) {
	if float64(f) == float64(int(f)) {
		return []byte(strconv.FormatFloat(float64(f), 'f', 1, 32)), nil
	}
	return []byte(strconv.FormatFloat(float64(f), 'f', -1, 32)), nil
}


type Product struct {
	Name  string
	Price KeepZero
}


func main() {

	pro := Product{
		Name: "abc",
		Price: 0.000,
	}

	jsonStu, err := json.Marshal(pro)
	if err != nil {
		fmt.Println("生成json字符串错误")
	}

	//jsonStu是[]byte类型，转化成string类型便于查看
	fmt.Println(string(jsonStu))
}