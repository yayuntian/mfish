package com.ysten.example.yayun.domain;

import lombok.Data;
import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;

import java.util.List;

@Data
@Document(collection = "sourcePS")
public class SourcePs {
    @Id
    private String id;
    private String source;
    private List<PsOutSide> outSideSource;
    private String type;
    private List<String> contentType;
    private String name;
    private String originName;
    private String aliasName;
    private String timeLen;
    private String zone;
    private String language;
    private String years;
    private String premiereTime;
    private String worldPremiere;
    private String mainlandPremiere;
    private List<PsStar> director;
    private List<PsStar> scriptWriter;
    private List<PsStar> producer;
    private List<PsStar> superviser;
    private List<PsStar> leadingRole;
    private List<PsRoleMapping> roleMapping;
    private List<String> tags;
    private String poster;
    private String updateCycle;
    private String score;
    private String doubanScore;
    private String doubanDetailUrl;
    private String playCounts;
    private String hot;
    private List<PsAwards> awards;
    private String tvStation;
    private String cpCode;
    private String shortDesc;
    private String detailsUrl;
    private String playUrl;
    private String imdbUrl;
    private String setCounts;
    private String desc;
    private String date;
    private String creatTime;
    private String lastModify;
    private String isUpdate;

    public String middlePosterAddr;

    public String smallPosterAddr;

    public String squarePosterAddr;

    public String horizontalPoster;

    /**
     * 是否管理基准库 1：已关联 0:未关联  2:关联到相似
     */
    public Integer isRelatedBase;

    /**
     * 关联方式
     */
    private String relationMode;

    /**
     * 1：可以生产基准 0：不能生成基准
     */
    private Integer isCanMakeBase = 1;

    private String checkId;

}
