import MenuBar from '../components/MenuBar'
import SearchBar from '../components/SearchBar';
import PinnedSubheaderList from './lists';

const MainPage = () => {

    const keywords = [
        { id: 1, title: "국가장학금 - 학사, 장학" },
        { id: 2, title: "개별연구 - 학사" },
        { id: 3, title: "근로장학 - 장학" },
        { id: 4, title: "계절학기 " }
    ];

    return (
        <div className="container">
            <div className="up"> 
                <SearchBar />
            </div>

            <div className="down">
                <div className="menubar">
                    <MenuBar keywords={keywords}></MenuBar>
                </div>

                <div className="component-wrapper">

                <div className="row1">
                    <div className="component-container">
                        <h5>&nbsp; 일반 </h5> 
                        <PinnedSubheaderList Cid={1} />
                    </div>

                    <div className="component-container">
                        <h5>&nbsp; 학사 </h5>
                        <PinnedSubheaderList Cid={2}/>
                    </div>
                </div>

                <div className="row2">
                    <div className="component-container">
                        <h5>&nbsp; 장학 </h5>
                        <PinnedSubheaderList Cid={3}/>
                    </div>

                    <div className="component-container">
                        <h5>&nbsp; 입시 </h5>
                        <PinnedSubheaderList Cid={4}/>
                    </div>
                </div>

                </div>
            </div>
    </div>
    )
}

export default MainPage;