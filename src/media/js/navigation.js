(function(){
// handler for when they click a category div
var handleCategoryClick = function(){
    $("div.items").hide();
    $(this).children("div.items").show();
    $("div.category").removeClass("selected");
    $(this).addClass("selected");
}

var addShadow = function(){
    var el = this;
    var outerDiv=null, innerDiv;
    var parentDiv;
    for(var i=0; i < 4; i++){
        innerDiv = document.createElement("div");
        innerDiv.style.paddingBottom = 1;
        innerDiv.style.paddingRight = 1;
        innerDiv.style.padding = "0px 1px 1px 0px";
        innerDiv.style.backgroundColor = ["#cccccc","#aaaaaa", "#888888", "#666666"][i];
        if(outerDiv)
            outerDiv.appendChild(innerDiv);
        else
            parentDiv = innerDiv;
        outerDiv = innerDiv;
    }
    el.parentNode.replaceChild(parentDiv, el);
    innerDiv.appendChild(el);
    el.style.backgroundColor = "white";
}

var init = function(){
    $("div.category").click(handleCategoryClick);
    // show the ones that are already selected
    $("div.category.selected div.items").show();
    $("div.shadow").each(addShadow);
}

$(document).ready(init);
})();

function setNavCategory(cat){
    $("div.category[name=" + cat + "]").click();
}
