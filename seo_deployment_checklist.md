# SEO Deployment Checklist

## Pre-deployment ✅
- [x] Run `python manage.py check`
- [x] Test locally with `python test_seo_simple.py`
- [x] Review all changes in git
- [ ] Backup production database

## Deployment ✅
- [x] Push changes to production
- [ ] Wait for deployment completion
- [ ] Test live site with `python test_live_seo.py`

## Post-deployment
- [ ] Submit updated sitemap to Google Search Console
- [ ] Test all major pages for SEO elements
- [ ] Check mobile usability
- [ ] Monitor Core Web Vitals
- [ ] Verify structured data with Google's Rich Results Test
- [ ] Check robots.txt and ads.txt accessibility

## Monitoring (first week)
- [ ] Monitor search rankings
- [ ] Check for crawl errors in Search Console
- [ ] Review page speed insights
- [ ] Monitor organic traffic changes
- [ ] Check for any broken links

## Long-term (monthly)
- [ ] Review Search Console performance
- [ ] Update meta descriptions based on CTR
- [ ] Add new structured data as needed
- [ ] Optimize underperforming pages
