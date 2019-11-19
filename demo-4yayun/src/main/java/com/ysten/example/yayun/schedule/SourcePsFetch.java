package com.ysten.example.yayun.schedule;

import com.ysten.example.yayun.domain.SourcePs;
import com.ysten.example.yayun.service.SourcePsService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.scheduling.annotation.EnableScheduling;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;

import java.util.List;

@EnableScheduling
@Slf4j
@RequiredArgsConstructor
@Component
public class SourcePsFetch {
    private final SourcePsService sourcePsService;

//    @Scheduled(cron = "0/20 * * * * ?")
    @Scheduled(cron = "${systemParameters.scheduling.cron}")
    public void fetch() {
        log.info("====Hi YaYun, care the schedule begin fetch data from mongodb====");
        List<SourcePs> result = sourcePsService.find(0, 50);
        log.info("fetch result:{}.", result);
        log.info("====Hoo YaYun, care the schedule end fetch data from mongodb====");
    }
}
