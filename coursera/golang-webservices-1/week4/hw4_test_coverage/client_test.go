package main

import (
	"encoding/json"
	"encoding/xml"
	"fmt"
	"io"
	"io/ioutil"
	"net/http"
	"net/http/httptest"
	"sort"
	"strconv"
	"strings"
	"testing"
	"time"
)

// код писать тут
type Row struct {
	ID            int    `xml:"id"`
	Guid          string `xml:"guid"`
	IsActive      string `xml:"isActive"`
	Balance       string `xml:"balance"`
	Picture       string `xml:"picture"`
	Age           int    `xml:"age"`
	EyeColor      string `xml:"eyeColor"`
	FirstName     string `xml:"first_name"`
	LastName      string `xml:"last_name"`
	Gender        string `xml:"gender"`
	Company       string `xml:"company"`
	Email         string `xml:"email"`
	Phone         string `xml:"phone"`
	Address       string `xml:"address"`
	About         string `xml:"about"`
	Registered    string `xml:"registered"`
	FavoriteFruit string `xml:"favoriteFruit"`
}

type Root struct {
	Version string `xml:"version,attr"`
	List    []Row  `xml:"row"`
}

type ServerResponse struct {
	Status  int
	Content string
}

type TestCase struct {
	Token   string
	Request SearchRequest
	IsError bool
}

var dataSetLoc = `dataset.xml`

func LoadXML(datasetUrl string) []User {
	users := make([]User, 0)
	v := new(Root)
	xmlData, err := ioutil.ReadFile(datasetUrl)
	if err != nil {
		panic(fmt.Sprintf("cannot read xml located in %v with err: %v", datasetUrl, err))
	}

	err = xml.Unmarshal(xmlData, &v)
	if err != nil {
		panic(fmt.Sprintf("error during unmarshal xml: %v", err))
	}

	for _, u := range v.List {
		users = append(users, User{
			Id:     u.ID,
			Name:   u.FirstName + " " + u.LastName,
			Age:    u.Age,
			About:  u.About,
			Gender: u.Gender,
		})
	}
	return users
}

func isValidOrderField(order_field string) bool {
	switch order_field {
	case
		"Id",
		"Age",
		"Name",
		"":
		return true
	}
	return false
}

func makeResponse(w http.ResponseWriter, response ServerResponse) {
	w.WriteHeader(response.Status)
	if _, err := io.WriteString(w, response.Content); err != nil {
		panic(fmt.Sprintf("error during makeResponse: %v", err))
	}
}

func getMockForToken(accessToken string) ServerResponse {
	switch accessToken {
	case "500":
		return ServerResponse{http.StatusInternalServerError, ""}
	case "401":
		return ServerResponse{http.StatusUnauthorized, ""}
	case "400_bad_json":
		return ServerResponse{http.StatusBadRequest, `{ "Error": "wrong json" `}
	case "200_bad_json":
		return ServerResponse{http.StatusOK, `{ "Error": "wrong json" `}
	case "400_unknown":
		errString, _ := json.Marshal(SearchErrorResponse{Error: "hello, this is unknown error"})
		return ServerResponse{http.StatusBadRequest, string(errString)}
	case "timeout":
		time.Sleep(30 * time.Second)
		return ServerResponse{0, ""}
	}
	return ServerResponse{0, ""}
}

func SearchServer(w http.ResponseWriter, r *http.Request) {
	users := LoadXML(dataSetLoc)

	accessToken := r.Header.Get("AccessToken")
	mockResponse := getMockForToken(accessToken)
	if mockResponse.Status != 0 {
		makeResponse(w, mockResponse)
		return
	}

	limit, _ := strconv.Atoi(r.FormValue("limit"))
	offset, _ := strconv.Atoi(r.FormValue("offset"))
	query := r.FormValue("query")
	order_field := r.FormValue("order_field")
	order_by, _ := strconv.Atoi(r.FormValue("order_by"))

	if !isValidOrderField(order_field) {
		errString, _ := json.Marshal(SearchErrorResponse{Error: "ErrorBadOrderField"})
		makeResponse(w, ServerResponse{http.StatusBadRequest, string(errString)})
		return
	}

	if order_by != 0 {
		sort.Slice(users, func(i, j int) bool {
			switch order_by {
			case -1:
				i, j = j, i
			}
			switch order_field {
			case "Id":
				return users[i].Id < users[j].Id
			case "Age":
				return users[i].Age < users[j].Age
			}
			return users[i].Name < users[j].Name
		})
	}

	result := make([]User, 0, limit)
	for _, u := range users {
		if strings.Contains(u.Name, query) {
			if offset > 0 {
				offset--
				continue
			}
			if len(result) < limit {
				result = append(result, u)
			} else {
				break
			}
		}
	}
	content, _ := json.Marshal(result)
	makeResponse(w, ServerResponse{http.StatusOK, string(content)})
}

func TestClientResponse(t *testing.T) {
	cases := []TestCase{
		TestCase{
			Token:   "500",
			IsError: true,
		},
		TestCase{
			Token:   "401",
			IsError: true,
		},
		TestCase{
			Token:   "400_bad_json",
			IsError: true,
		},
		TestCase{
			Token:   "200_bad_json",
			IsError: true,
		},
		TestCase{
			Token:   "400_unknown",
			IsError: true,
		},
		TestCase{
			Token:   "timeout",
			IsError: true,
		},
		TestCase{
			Token:   "limit_below_zero",
			IsError: true,
			Request: SearchRequest{
				Limit:      -1,
				Offset:     0,
				Query:      "",
				OrderField: "",
				OrderBy:    0,
			},
		},
		TestCase{
			Token:   "offset_below_zero",
			IsError: true,
			Request: SearchRequest{
				Limit:      0,
				Offset:     -1,
				Query:      "",
				OrderField: "",
				OrderBy:    0,
			},
		},
		TestCase{
			Token:   "change_limit",
			IsError: true,
			Request: SearchRequest{
				Limit:      26,
				Offset:     -1,
				Query:      "",
				OrderField: "",
				OrderBy:    0,
			},
		},
		TestCase{
			Token:   "wrong_order_field",
			IsError: true,
			Request: SearchRequest{
				Limit:      0,
				Offset:     0,
				Query:      "",
				OrderField: "hello",
				OrderBy:    0,
			},
		},
		TestCase{
			Token:   "wrong_url",
			IsError: true,
			Request: SearchRequest{
				Limit:      0,
				Offset:     0,
				Query:      "",
				OrderField: "",
				OrderBy:    0,
			},
		},
		TestCase{
			Token:   "only_one",
			IsError: false,
			Request: SearchRequest{
				Limit:      1,
				Offset:     0,
				Query:      "Lynn",
				OrderField: "Name",
				OrderBy:    0,
			},
		},
		TestCase{
			Token:   "more",
			IsError: false,
			Request: SearchRequest{
				Limit:      1,
				Offset:     0,
				Query:      "a",
				OrderField: "Name",
				OrderBy:    0,
			},
		},
	}

	ts := httptest.NewServer(http.TimeoutHandler(http.HandlerFunc(SearchServer), 1*time.Second, ""))

	for caseNum, item := range cases {
		url := ts.URL
		if item.Token == "wrong_url" {
			url = "blabla"
		}
		c := &SearchClient{
			AccessToken: item.Token,
			URL:         url,
		}
		_, err := c.FindUsers(item.Request)

		if err == nil && item.IsError {
			t.Errorf("[%d] expected error, got nil", caseNum)
		}
		if err != nil && !item.IsError {
			t.Errorf("[%d] unexpected error: %#v", caseNum, err)
		}
	}
	ts.Close()
}
