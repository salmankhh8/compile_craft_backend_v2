function frequency_check(str){;
;
    obj={};
;
    for(let i=0; i<str.length; i++){;
        obj[str[i]] = (obj[str[i]] || 0) + 1 ;
    };
;
    return obj;
};
;
;
console.log(JSON.stringify(frequency_check("ihughjklihugyvyfcvf"), null, 2))